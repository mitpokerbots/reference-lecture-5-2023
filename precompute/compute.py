import eval7
import itertools
import pandas as pd 


def calculate_strength(self, hole, iterations):
    
        deck = eval7.Deck()
        hole_card = [eval7.Card(card) for card in hole]

        for card in hole_card:
            deck.cards.remove(card)

        score = 0

        for _ in range(iterations):
            deck.shuffle()

            _COMM = 5
            _OPP = 2

            draw = deck.peek(_COMM + _OPP)

            opp_hole = draw[:_OPP]
            community = draw[_OPP:]

            our_hand = hole_card +  community
            opp_hand = opp_hole +  community

            our_value = eval7.evaluate(our_hand)
            opp_value = eval7.evaluate(opp_hand)

            if our_value > opp_value:
                score += 2
            
            elif our_value == opp_value:
                score += 1

            else:
                score += 0

        hand_strength = score / (2 * iterations)

        return hand_strength


if __name__ == '__main__':

    _MONTE_CARLO_ITERS = 100000
    _RANKS = 'AKQJT98765432'

    off_rank_holes = list(itertools.combinations(_RANKS, 2)) #all holes we can have EXCEPT pocket pairs (e.g. [(A, K), (A, Q), (A, J)...])
    pocket_pair_holes = list(zip(_RANKS, _RANKS)) #all pocket pairs [(A, A), (K, K), (Q, Q)...]

    suited_strengths = [calculate_strength([hole[0] + 'c', hole[1] + 'c'], _MONTE_CARLO_ITERS) for hole in off_rank_holes] #all holes with the same suit
    off_suit_strengths = [calculate_strength([hole[0] + 'c', hole[1] + 'd'], _MONTE_CARLO_ITERS) for hole in off_rank_holes] #all holes with off suits
    pocket_pair_strengths = [calculate_strength([hole[0] + 'c', hole[1] + 'd'], _MONTE_CARLO_ITERS) for hole in pocket_pair_holes] #pocket pairs must be off suit

    suited_holes = [hole[0] + hole[1] + 's' for hole in off_rank_holes] #s == suited
    off_suited_holes = [hole[0] + hole[1] + 'o' for hole in off_rank_holes] #o == off-suit
    pocket_pairs = [hole[0] + hole[1] + 'o' for hole in pocket_pair_holes] #pocket pairs are always off suit

    all_strengths = suited_strengths + off_suit_strengths + pocket_pair_strengths #aggregate them all
    all_holes = suited_holes + off_suited_holes + pocket_pairs

    hole_df = pd.DataFrame() #make our spreadsheet with a pandas data frame!
    hole_df['Holes'] = all_holes
    hole_df['Strengths'] = all_strengths

    hole_df.to_csv('hole_strengths.csv', index=False) #save it for later use, trade space for time!