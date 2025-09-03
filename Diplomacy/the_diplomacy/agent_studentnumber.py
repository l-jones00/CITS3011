import time
import timeout_decorator
import heapq #for A*
from collections import defaultdict
from agent_baselines import Agent

#so i can refer to the attribute, rather than num so I don't mess it up
FRIENDLY, NEUTRAL, HOSTILE = 0, 1, 2

class AttitudeModel:
    def __init__(self, powers, self_power):
        self.self_power = self_power
        self.others = [p for p in powers if p != self_power]
        # for each power, give a percentage friendly/neutral/hostile STARTING OPTIMISTIC
        self.post = {p: [0.55, 0.35, 0.10] for p in self.others}
        # transition table - rows = previous, cols = next, 
        self.T = {
            'AttackedBySuccess':  [[0.00, 0.20, 0.80],[0.00, 0.10, 0.90],[0.00, 0.00, 1.00]],
            'AttackedBy':         [[0.00, 0.50, 0.50],[0.00, 0.30, 0.70],[0.00, 0.00, 1.00]],
            'SupportedBySuccess': [[1.00, 0.00, 0.00],[0.60, 0.40, 0.00],[0.10, 0.70, 0.20]],
            'SupportedBy':        [[1.00, 0.00, 0.00],[0.20, 0.70, 0.10],[0.00, 0.30, 0.70]],
        }
    
    def hostile_prob(self, p):
        return self.post[p][HOSTILE]
    
    def friendly_prob(self, p):
        return self.post[p][FRIENDLY]
    
    def apply(self, p, key):
        prev = self.post[p]
        
        T = self.T[key]
        nxt = [0.0, 0.0, 0.0]
        for i in range(3):
            for j in range(3):
                nxt[j] += prev[i] * T[i][j]
        s = sum(nxt); self.post[p] = [x/s for x in nxt]

    #Call after processing a movement phase to check what others did to us
    def update_from(self, game_after, all_power_orders, our_units_before, our_locs_before):
        for p in self.others:
            
            flags = {
                'AttackedBySuccess':False,
                'AttackedBy':False,
                'SupportedBySuccess':False,
                'SupportedBy':False,
                'Other':True
            }

            orders = all_power_orders.get(p, [])
            status = game_after.get_order_status(power_name=p) 
            #returns a dict like : {"A MUN" : [], "F KIE": ["void"]} where non-empty indicates failure reason

            for order in orders:
                if '-' not in order and ' S ' not in order: # only consider move/attack/support orders
                    continue
                words = order.split()
                if not words: continue

                unit = ' '.join(words[:2])

                #MOVE/ATTACKS
                if '-' in words:
                    try: target = words[words.index('-')+1]
                    except: target = None

                    if target in our_locs_before:
                        flags['AttackedBy'] = True
                        if status.get(unit, None) == []:
                            flags['AttackedBySuccess']

                #SUPPORT
                if 'S' in words:
                    try: supported_unit = ' '.join([words[words.index('S')+1], words[words.index('S')+2]])
                    except: supported_unit = None

                    if supported_unit in our_units_before:
                        flags['SupportedBy'] = True
                        if status.get(unit, None) == []:
                            flags['SupportedBySuccess'] = True
                
                #PRIORITY TO APPLY ONLY ONE ACTION
                for key in ['AttackedBySuccess','AttackedBy','SupportedBySuccess','SupportedBy']:
                    if flags[key]:
                        self._apply(p, key)
                        break


class StudentAgent(Agent):
    '''
    Implement your agent here. 

    Please read the abstract Agent class from baseline_agents.py first.
    
    You can add/override attributes and methods as needed.
    '''

    #@timeout_decorator.timeout(1)
    def __init__(self, agent_name='Heuristic + Attitude'):
        super().__init__(agent_name)
        self.attitude = None
         

    #@timeout_decorator.timeout(1)
    def new_game(self, game, power_name):
        self.game = game
        self.power_name = power_name
        self.attitude = AttitudeModel(list(self.game.powers.keys()), power_name)


    #@timeout_decorator.timeout(1) # This is only for updating the game engine and other states if any. Do not implement heavy stratergy here.
    def update_game(self, all_power_orders):
        movement = (self.game.phase_type == 'M')
        if movement:
            our_centers = set(self.game.get_centers(self.power_name))
            our_units_locs = set(self.game.get_orderable_locations(self.power_name))
            our_locs_before = our_centers | our_units_locs
            our_units_before = set(self.game.get_units(self.power_name))

        # do not make changes to the following codes
        for power_name in all_power_orders.keys():
            self.game.set_orders(power_name, all_power_orders[power_name])
        self.game.process()

        #update attitudes after moves resolve
        if movement:
            self.attitude.update_from(self.game, all_power_orders, our_locs_before, our_units_before)

    ####################################################################################################################################
    #           HELPER FUNCTIONS            #
    ####################################################################################################################################

    def _is_simple_move(self, order):
        word = order.split()
        return ('-' in word) and (' S ' not in order) and (' C ' not in order) and (' VIA' not in order)

    def _move_target(self, order):
        word = order.split()
        return word[word.index('-') + 1]

    def season(self):
        phase = self.game.get_current_phase()
        return phase[0] if phase else 'S' #return S as a default i.e. spring if for some reason there's no phase
    
    def is_sc(self, loc):
        return loc in self.game.map.scs #list of all SC locations e.g. LON, PAR, VIE etc
    
    def hostile_pressure(self, loc):
        pressure = 0.0
        for p in self.game.powers.keys():
            if p == self.power_name: continue
            h = self.attitude.hostile_prob(p) if self.attitude else 0.33 #just give a third chance if there's nothing initalised to begin with
            for unit in self.game.get_units(p):
                utype, u_loc = unit.split(' ', 1)
                if self.game.map.abuts(utype, u_loc.upper(), '-', loc): #abuts: "can a unit of type utype move from "from" to "to" in one step"
                    pressure += max(0.25, h)  # minimum uncertainty
        return pressure
    
    def _unit_candidates(self, loc, topk=3):
        poss = self.game.get_all_possible_orders().get(loc, [])
        scored = sorted(poss, key=lambda o: self.order_local_score(loc, o), reverse=True)
        return scored[:topk]

    def _ub_remaining(self, remaining_locs):
        ub = 0.0
        all_poss = self.game.get_all_possible_orders()
        for loc in remaining_locs:
            cands = all_poss.get(loc, [])
            if not cands: continue
            best = max((self.order_local_score(loc, o) for o in cands), default=0.0)
            ub += best
        return ub
    ####################################################################################################################################
    #           POLICY FUNCTION            #
    ####################################################################################################################################

    def order_local_score(self, loc, order):
        words = order.split()
        if not words:
            return -10000000000000000
        
        season = self.season()
        val = 0.0

        is_move = '-' in words
        is_hold =  (len(words) >= 3 and words[2] == 'H') or (not is_move and 'S' not in words and 'C' not in words)
        target = None
        if is_move:
            try:
                target = words[words.index('-') + 1]
            except Exception:
                target = None
        
        if season == 'S':
            if target and self.is_sc(target): 
                val += 2.0
            if is_move:
                val += 0.5 #keep movement up
        elif season == 'F':
            if target and self.is_sc(target):
                val += 4.0
            if is_hold and self.is_sc(target):
                val += 2.0
        #elif season == 'W':
            #nothing for now

        #Danger Penality#

        end_location = (target or loc).upper() #normalise location name just in case
        danger = self.hostile_pressure(end_location)
        val -= 0.6*danger
        
        return val
    
    def _support_coordination_pass(self, orders):
    # collect simple moves by target
        moves_by_tgt = {}
        for od in orders:
            if self._is_simple_move(od):
                tgt = self._move_target(od)
                moves_by_tgt.setdefault(tgt, []).append(od)

        new_orders = orders[:]
        for tgt, lst in moves_by_tgt.items():
            if len(lst) < 2:
                continue
            # keep the first as mover; turn the rest into supports
            mover = lst[0]
            for supporter in lst[1:]:
                # supporter head "<A/F> <LOC>"
                w = supporter.split()
                head = f"{w[0]} {w[1]}"
                sup_order = f"{head} S {mover}"
                # replace exact supporter occurrence
                try:
                    j = new_orders.index(supporter)
                    new_orders[j] = sup_order
                except ValueError:
                    pass

        # de-dup preserve order
        seen, out = set(), []
        for od in new_orders:
            if od not in seen:
                seen.add(od)
                out.append(od)
        return out


    ####################################################################################################################################
    #           A* FUNCTION/s?            #
    ####################################################################################################################################

    def best_first_joint(self, time_budget=0.83, topk = 3, beam=180):
        start = time.time()
        orderable = self.game.get_orderable_locations(self.power_name)
        if not orderable: return []

        candidates = {loc: self._unit_candidates(loc, topk=topk) for loc in orderable}
        orderable.sort(key=lambda L: len(candidates.get(L, []))) #expand units with less candidates first to reduce branching

        # node: (-f, seq_id, idx, chosen_orders, g) which is put into pq
        # f = g+h (-f so python's min-heap pops largest f first)
        # seq = tie-breaker so heap order is stable even if f is tied
        # idx = num of units that have been assigned so far (index) = DEPTH
            # pop node with idx == k, the next unit to be assigned is orderable[k]
        # chosen = list of orders picked so far, one per unit in order
        # g = realised score of chosen

        seq = 0 
        need_order = orderable[:] #copy of the list of unit locations that need orders this phase
        h0 = self._ub_remaining(need_order) #optimistic upper bound if we haven't chosen anything yet - default i.e. sum of best local scores from each unit
        pq = [(-(h0), seq, 0, [], 0.0)] #priority queue, min heap!
        best = ([], -1e18) # keeps best full join plan we've seen so far (start very low so any joint order is better :)

        while pq and (time.time() - start) < time_budget:
            # beam control
            if len(pq) > beam:
                pq = heapq.nsmallest(beam, pq)
                heapq.heapify(pq)

            _, _, idx, chosen, g = heapq.heappop(pq)

            if idx == len(orderable):
                if g > best[1]:
                    best = (chosen, g)
                continue

            loc = orderable[idx]
            options = candidates.get(loc, [])
            if not options:
                # skip empty; continue with UB of rest
                h = self._ub_remaining(orderable[idx+1:])
                seq += 1
                heapq.heappush(pq, (-(g+h), seq, idx+1, chosen, g))
                continue

            for od in options: #generating new child
                # compute collision penalty vs. already-chosen moves
                pen = 0.0
                if self._is_simple_move(od):
                    tgt = self._move_target(od)
                    for prev in chosen:
                        if self._is_simple_move(prev) and self._move_target(prev) == tgt:
                            pen += 1.0  # tune: 0.5 ~ 1.5 works well
                g2 = g + self.order_local_score(loc, od) - pen
                g2 = g + self.order_local_score(loc, od)
                h2 = self._ub_remaining(orderable[idx+1:])
                f2 = g2 + h2
                seq += 1
                heapq.heappush(pq, (-(f2), seq, idx+1, chosen + [od], g2))

        return best[0] if best[0] else []

    3

    #@timeout_decorator.timeout(1)
    def get_actions(self):
        if self.game.phase_type == 'M':
            if self.season() == 'F':
                orders = self.best_first_joint(time_budget=0.5, topk=2, beam=120)
                if orders: 
                    orders = self._support_coordination_pass(orders)
                    return orders

        #If non-movement phase
        possible_by_loc = self.game.get_all_possible_orders()
        my_locs = self.game.get_orderable_locations(self.power_name)

        chosen = []
        for loc in my_locs:
            candidates = possible_by_loc.get(loc, [])
            if not candidates:
                continue
            chosen.append(max(candidates, key=lambda o: self.order_local_score(loc, o)))
       
        return chosen


























        '''
        Return a list of orders. Each order is a string, with specific format. For the format, read the game rule and game engine documentation.
        
        Expected format:
        A LON H                  # Army at LON holds
        F IRI - MAO              # Fleet at IRI moves to MAO (and attack)
        A WAL S F LON            # Army at WAL supports Fleet at LON (and hold)
        F NTH S A EDI - YOR      # Fleet at NTH supports Army at EDI to move to YOR
        F NWG C A NWY - EDI      # Fleet at NWG convoys Army at NWY to EDI
        A NWY - EDI VIA          # Army at NWY moves to EDI via convoy
        A WAL R LON              # Army at WAL retreats to LON
        A LON D                  # Disband Army at LON
        A LON B                  # Build Army at LON
        F EDI B                  # Build Fleet at EDI

        Note: If an invalid order is sent to the engine, it will be accepted but with a result of 'void' (no effect).
        Note: For a 'support' action, two orders are needed, one for the supporter and one for the supportee. (Same for 'convoy')
        Note: For each unit, if no order is given, it will 'hold' by default.

        Useful Functions:
        
        # This is a dict of all the possible orders for each unit at each location (for all powers).
        possible_orders = self.game.get_all_possible_orders()

        # This is a list of all orderable locations for the power you control.
        orderable_locations = self.game.get_orderable_locations(self.power_name)
    
        # Combining these two, you can have the full action space for the power you control.

        # You can re-use the build_map_graphs function in the GreedyAgent to build the connection graph of the map if needed.
        
        '''