const fs = require('fs');

const INPUT1 = fs.readFileSync('input1.txt', 'utf8');
const INPUT2 = fs.readFileSync('input2.txt', 'utf8');

const INSTRUCTIONS = {
    'addr': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] + inputs[B];
        return outputs;
    },

    'addi': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] + B;
        return outputs;
    },

    'mulr': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] * inputs[B];
        return outputs;
    },

    'muli': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] * B;
        return outputs;
    },

    'banr': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] & inputs[B];
        return outputs;
    },

    'bani': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] & B;
        return outputs;
    },

    'borr': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] | inputs[B];
        return outputs;
    },

    'bori': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] | B;
        return outputs;
    },

    'setr': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A];
        return outputs;
    },

    'seti': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = A;
        return outputs;
    },

    'gtir': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = A > inputs[B] ? 1 : 0;
        return outputs;
    },

    'gtri': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] > B ? 1 : 0;
        return outputs;
    },

    'gtrr': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] > inputs[B] ? 1 : 0;
        return outputs;
    },

    'eqir': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = A == inputs[B] ? 1 : 0;
        return outputs;
    },

    'eqri': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] == B ? 1 : 0;
        return outputs;
    },

    'eqrr': (A, B, C, inputs) => {
        outputs = inputs.slice();
        outputs[C] = inputs[A] == inputs[B] ? 1 : 0;
        return outputs;
    },
};

String.prototype.getNumbers = function () {
    var rx = /[+-]?((\.\d+)|(\d+(\.\d+)?)([eE][+-]?\d+)?)/g,
        mapN = this.match(rx) || [];
    return mapN.map(Number);
};

function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;

    // If you don't care about the order of the elements inside
    // the array, you should sort both arrays here.
    // Please note that calling sort on an array will modify that array.
    // you might want to clone your array first.

    for (let i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) return false;
    }
    return true;
}

function findPossibleOpcodes(before, instruction, after) {
    const possibleOpcodes = [];
    for (let [opcode, fn] of Object.entries(INSTRUCTIONS)) {
        const [code, A, B, C] = instruction;
        const result = fn(A, B, C, before);
        if (arraysEqual(result, after)) {
            possibleOpcodes.push(opcode);
        }
    }
    return possibleOpcodes;
}

let before, instruction;
let count = 0;
INPUT1.split('\n').forEach(line => {
    if (line.indexOf('Before') !== -1) {
        before = line.getNumbers();
    }
    else if (line.indexOf('After') !== -1) {
        const after = line.getNumbers();
        const opcodes = findPossibleOpcodes(before, instruction, after);
        if (opcodes.length >= 3) {
            count += 1;
        }
    }
    else {
        instruction = line.getNumbers();
    }
});
console.log(count);
