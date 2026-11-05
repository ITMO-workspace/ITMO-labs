package web.models;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;

/**
* Model object for Point with coordinates check implementation
* @author Septyq
*/

public class RestrainedPoint extends Point {
    private ArrayList<BigInteger> yValues = new ArrayList<>(Arrays.asList(
        new BigInteger("-4"), new BigInteger("-3"), new BigInteger("-2"), new BigInteger("-1"),
        new BigInteger("0"), new BigInteger("1"), new BigInteger("2"), new BigInteger("3"), new BigInteger("4")
    ));

    private ArrayList<BigDecimal> rValues = new ArrayList<>(Arrays.asList(
        new BigDecimal("1"), new BigDecimal("1.5"), new BigDecimal("2"), new BigDecimal("2.5"), new BigDecimal("3")
    ));

    public RestrainedPoint(String x, String y, String r) throws NumberFormatException {
        super(x, y, r);
    }

    public boolean coordsOk() {
        return this.x.compareTo(new BigDecimal(-3)) > 0 && this.x.compareTo(new BigDecimal(3)) < 0 &&
                this.yValues.contains(this.y) &&
                this.rValues.contains(this.r);
    }

    public BigInteger parseInteger(String value) {
        return new BigInteger(value);
    };
    public BigDecimal parseDecimal(String value) {
        return new BigDecimal(value.replace(",", "."));
    };

}
