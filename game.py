from player import Player
from deck import Deck


class Game:
    turn = -1
    players = []
    deck = Deck()

    def start(self):
        number_of_players = "0"
        while number_of_players not in "23456":
            number_of_players = input("How many players (2-6): ")

        for i in range(int(number_of_players)):
            name = input("Name for player {}: ".format(i + 1))
            self.players.append(Player(self, name, i))

    def next_turn(self):
        self.turn += 1
        print("======================================================")
        for player in self.players:
            print([player.name, player.coins, len(player.cards)])
        print(self.current_player.cards)
        print("======================================================")

    @property
    def over(self):
        return len(self.players) == 1

    @property
    def current_player(self):
        return self.players[self.turn % len(self.players)]

    def next_player(self, player):
        next_seat = (player.seat + 1) % len(self.players)
        return self.players[next_seat]

    def round_of_challenges(self, player, action):
        challenging_player = self.next_player(player)
        while challenging_player is not player:
            if challenging_player.performs_challenge():
                if player.pass_challenge(action):
                    challenging_player.loose_life()
                    action.resolve()
                    return True, True
                else:
                    player.loose_life()
                    return True, False

            challenging_player = game.next_player(challenging_player)

        return False, False

    def remove_player(self, player):
        self.players.remove(player)

if __name__ == "__main__":
    game = Game()
    game.start()
    while not game.over:
        game.next_turn()
        end_turn = False

        current_player = game.current_player

        selected_action = current_player.request_action()
        victim = None
        if selected_action.requires_victim:
            victim = current_player.select_victim()

        selected_action = selected_action(current_player, victim)

        if selected_action.can_be_challenged:
            end_turn, current_player_won = game.round_of_challenges(current_player, selected_action)
            if end_turn:
                continue  # Next turn

        if selected_action.can_be_blocked is True:
            blocking_player = game.next_player(current_player)
            while blocking_player is not game.current_player:
                if blocking_player.performs_block():
                    blocking_action = selected_action.blocked_by(blocking_player)
                    end_turn, blocking_player_won = game.round_of_challenges(blocking_player, blocking_action)
                    if end_turn and blocking_player_won:
                        break  # Next turn
                    if end_turn:
                        selected_action.resolve()
                        break

                blocking_player = game.next_player(blocking_player)

        selected_action.resolve()

    print("Game Over!!, Winner is {}".format(game.players[0]))