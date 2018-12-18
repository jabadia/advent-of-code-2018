const fs = require('fs');

const INPUT1 = fs.readFileSync('input1.txt', 'utf8');
const INPUT2 = fs.readFileSync('input2.txt', 'utf8');

const INSTRUCTIONS = {
    'addr': (A, B, C, registers) => {
        registers[C] = registers[A] + registers[B];
    },

    'addi': (A, B, C, registers) => {
        registers[C] = registers[A] + B;
    },

    'mulr': (A, B, C, registers) => {
        registers[C] = registers[A] * registers[B];
    },

    'muli': (A, B, C, registers) => {
        registers[C] = registers[A] * B;
    },

    'banr': (A, B, C, registers) => {
        registers[C] = registers[A] & registers[B];
    },

    'bani': (A, B, C, registers) => {
        registers[C] = registers[A] & B;
    },

    'borr': (A, B, C, registers) => {
        registers[C] = registers[A] | registers[B];
    },

    'bori': (A, B, C, registers) => {
        registers[C] = registers[A] | B;
    },

    'setr': (A, B, C, registers) => {
        registers[C] = registers[A];
    },

    'seti': (A, B, C, registers) => {
        registers[C] = A;
    },

    'gtir': (A, B, C, registers) => {
        registers[C] = A > registers[B] ? 1 : 0;
    },

    'gtri': (A, B, C, registers) => {
        registers[C] = registers[A] > B ? 1 : 0;
    },

    'gtrr': (A, B, C, registers) => {
        registers[C] = registers[A] > registers[B] ? 1 : 0;
    },

    'eqir': (A, B, C, registers) => {
        registers[C] = A === registers[B] ? 1 : 0;
    },

    'eqri': (A, B, C, registers) => {
        registers[C] = registers[A] === B ? 1 : 0;
    },

    'eqrr': (A, B, C, registers) => {
        registers[C] = registers[A] === registers[B] ? 1 : 0;
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
        fn(A, B, C, before);
        if (arraysEqual(before, after)) {
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
