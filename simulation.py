class Simulation:
    def __init__(self, blocks):
        self._blocks = blocks
        self._finished = False

    def run(self):
        while not self._finished:
            self._step()

    def _step(self):
        visited = set()
        queue = [b for b in self._blocks if not b.inputs]
        nothing_changed = True
        while queue:
            block = queue.pop()
            if block in visited:
                continue

            outputs_before = [c.value for c in block.outputs]
            block.push()
            outputs_after = (c.value for c in block.outputs)
            nothing_changed &= all(x == y for x, y in zip(outputs_after, outputs_before))

            queue.extend((k.block for c in block.outputs for k in c.connections))
            visited.add(block)
        self._finished = nothing_changed
