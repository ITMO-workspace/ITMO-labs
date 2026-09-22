import { CartesianValue } from './CartesianValue.js';

export class XCoordinate extends CartesianValue {
    #possibleValues = [-3, -2. -1, 0, 1, 2, 3, 4, 5]

    parseValue(value) {
        return parseFloat(value);
    }

    validate() {
        return (this.value != null) && this.isNumeric(this.value) && this.#possibleValues.includes(this.value);
    }
}