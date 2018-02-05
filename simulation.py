class Simulation:
    def __init__(self, blocks):
        self._blocks = blocks

    def run(self):
        visited = set()
        queue = [b for b in self._blocks if not b.inputs]

        while queue:
            block = queue.pop(0)
            if block in visited:
                continue
            block.push()
            queue.extend((k.block for c in block.outputs for k in c.connections))
            visited.add(block)
