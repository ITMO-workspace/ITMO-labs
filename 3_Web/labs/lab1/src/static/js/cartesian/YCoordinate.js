import { CartesianValue } from './CartesianValue.js';

export class YCoordinate extends CartesianValue {
    validate() {
        if (this.value === "" || this.value === undefined) {
            return false;
        }
        if (!this.isNumeric(this.value)) {
            return false;
        }
        if (this.value < -5 || this.value > 5) {
            return false;
        }
        return true;
    }

    parseValue(value) {
        return parseFloat(value);
    }
}