from block import source, operator_of, nor, display_block


def sources(*args):
    return tuple(source(v) for v in args)


def rs_flip_flop(initial_q=0, initial_s=1, x=0, y=0):
    source_s, source_r = sources(initial_s, initial_q)
    nor1 = operator_of(nor, source_s)
    nor2 = operator_of(nor, nor1, source_r)
    nor2.outputs[0].connect_with(nor1.inputs[1])
    display_q = operator_of(display_block, nor1)
    display_not_q = operator_of(display_block, nor2)

    source_s.translate((x + 50, y + 88))
    source_r.translate((x + 50, y + 212))
    nor1.translate((x + 200, y + 100))
    nor2.translate((x + 200, y + 200))
    display_q.translate((x + 350, y + 100))
    display_not_q.translate((x + 350, y + 200))

    return nor1, nor2, source_r, source_s, display_q, display_not_q
