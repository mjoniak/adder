# adder
Logic gate simulator written in Python

## Goal

The project aims to create a very simple simulation environment in which you can connect logic gates (blocks) and calculate state of the system.

## Areas

The space is composed of two main areas:

1. **Toolbox**: A list of elements to use. Contains some logic gates and an example flip-flop. Double click to place an element on the worksheet.
2. **Worksheet**: The simulation area. You can move the placed blocks by dragging them. You can also connect elements by clicking on one block's *output connector* and then on another block's *input connector*. You can click the *simulation button* to evaluate state.

## Blocks

Every block is represented as a rectangle with a label. Also, every block can have:

* Input connectors: on the block's left side. 
* Output connectors: on the block's right side.

To feed value from one block's output to another's input, just click on the output connector and then on the input connector. A connecting line should appear.

A block performs some logical operation (e.g. AND, OR, XOR, NAND, NOR) on values from the input connectors and forwards the result to the output connectors.

## Special elements

There are two types of special elements:

1. **Source block**: Produces a signal of 1 or 0. Double click on the block to switch state. Doesn't have any input connectors.
2. **Display block**: Displays it's input signal as a label. Doesn't have any output connectors.

## Example

Double click the RS flip-flop button and then click on *Run simulation*. Change the values on the leftmost source blocks and see how the state changes.