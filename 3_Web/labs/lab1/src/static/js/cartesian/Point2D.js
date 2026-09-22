import { CartesianValue } from './CartesianValue.js';
import { XCoordinate } from './XCoordinate.js';
import { YCoordinate } from './YCoordinate.js';
import { Radius } from './Radius.js';

export class Point2D extends CartesianValue {
    #value = {
        x: new XCoordinate(), 
        y: new YCoordinate(),
        r: new Radius()
    }
    #inAreaMethod;


    constructor(value, inAreaMethodImpl) {
        super(value);
        this.#inAreaMethod = inAreaMethodImpl;
    }

    static fromArray([x, y, r], inAreaMethodImpl) {
        value = {
            x: new XCoordinate(x), 
            y: new YCoordinate(y),
            r: new Radius(r)
        }
        return new Point2D(value, inAreaMethodImpl)
    }

    parseValue(value) {
        return value !== null
        && typeof value === 'object'
        && 'x' in value
        && 'y' in value
        && 'r' in value;
    } 

    validate() {
        return this.#value.x.validate() 
        && this.#value.y.validate() 
        && this.#value.r.validate();
    }

    inArea() {
        // console.log(this.#value.x, this.#value.y, this.#value.r, this.#inAreaMethod(this.#value.x, this.#value.y, this.#value.r))
        return this.#inAreaMethod(this.#value.x.value, this.#value.y.value, this.#value.r.value);
    }

    get value() {
        return this.#value;
    }

    set x(value) {
        this.#value.x = new XCoordinate(value);
    }

    set y(value) {
        this.#value.y = new YCoordinate(value);
    }

    set r(value) {
        this.#value.r = new Radius(value);
    }
}