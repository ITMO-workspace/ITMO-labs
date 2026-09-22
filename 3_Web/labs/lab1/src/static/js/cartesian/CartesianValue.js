export class CartesianValue {
    #value = 0;

    constructor (value) {
        this.#value = this.parseValue(value);
    }

    set value (value) {
        this.#value = this.parseValue(value);
    }

    get value() {
        return this.#value;
    }

    parseValue(value) {
        return value;
    }

    validate() {
        return (this.#value != null) && this.isNumeric(this.#value);
    }

    isNumeric(n) {
        return !isNaN(parseFloat(n)) && isFinite(n);
    }
}