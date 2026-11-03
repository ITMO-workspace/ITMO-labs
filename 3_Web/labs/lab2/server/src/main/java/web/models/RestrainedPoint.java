package web.models;

/**
* Model object for Point with coordinates check implementation
* @author Septyq
*/

public class RestrainedPoint extends Point {
    public RestrainedPoint(double x, double y, double r) {
        super(x, y, r);
    }

    public boolean coordsOk() {
        return this.x < 3 && this.x > -3;
    }
}
