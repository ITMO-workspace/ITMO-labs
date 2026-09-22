import { CartesianValue } from './CartesianValue.js';

export class Radius extends CartesianValue {
    #possibleValues = [1, 1.5, 2, 2.5, 3];

    parseValue(value) {
        return parseFloat(value);
    }

    validate() {
        return (this.value != null) && this.isNumeric(this.value) && this.#possibleValues.includes(this.value);
    }
}