from c4.evaluate import INF
from c4.engine.alphabeta import AlphaBetaEngine


class PVSEngine(AlphaBetaEngine):
    def search(self, board, depth, ply=1, alpha=-INF, beta=INF):
        self.inc('nodes')

        if board.end is not None:
            return self.endscore(board, ply)

        if depth <= 0:
            self.inc('leaves')
            return [], self.evaluate(board)

        bestmove = []
        bestscore = alpha
        for i, m in enumerate(self.moveorder(board, board.moves())):
            if i == 0 or depth == 1 or (beta-alpha) == 1:
                nextmoves, score = self.search(board.move(m), depth-1, ply+1,
                                               -beta, -bestscore)
            else:
                # pvs uses a zero window for all the other searches
                _, score = self.search(board.move(m), depth-1, ply+1,
                                       -bestscore-1, -bestscore)
                score = -score
                if score > bestscore:
                    nextmoves, score = self.search(board.move(m), depth-1, ply+1,
                                                   -beta, -bestscore)
                else:
                    continue

            score = -score
            if score > bestscore:
                bestscore = score
                bestmove = [m] + nextmoves
            elif not bestmove:
                bestmove = [m] + nextmoves

            if bestscore >= beta:
                self.inc('betacuts')
                break

        return bestmove, bestscore

    def __str__(self):
        return 'PVS(%s)' % self._maxdepth
