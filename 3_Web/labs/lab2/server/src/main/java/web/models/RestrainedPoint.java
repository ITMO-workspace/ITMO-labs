package web.models;

import java.math.BigDecimal;
import java.math.BigInteger;

/**
* Model object for Point with coordinates check implementation
* @author Septyq
*/

public class RestrainedPoint extends Point {
    public RestrainedPoint(String x, String y, String r) throws NumberFormatException {
        super(x, y, r);
    }

    public boolean coordsOk() {
        return this.x.compareTo(new BigDecimal(-3)) > 0 && this.x.compareTo(new BigDecimal(3)) < 0;
    }

    public BigInteger parseInteger(String value) {
        return new BigInteger(value);
    };
    public BigDecimal parseDecimal(String value) {
        return new BigDecimal(value.replace(",", "."));
    };

}
