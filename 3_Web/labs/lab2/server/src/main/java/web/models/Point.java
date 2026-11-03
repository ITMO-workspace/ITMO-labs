package web.models;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Objects;

/**
* Abstract model object for Point
* @author Septyq
*/

public abstract class Point {
  protected final BigDecimal x;
  protected final BigInteger y;
  protected final BigInteger r;

  protected final boolean isInArea;

  public Point(String x, String y, String r) throws NumberFormatException {
    this.x = parseDecimal(x);
    this.y = parseInteger(y);
    this.r = parseInteger(r);
    this.isInArea = isInside(this.x, this.y, this.r);
  }

  private boolean isInside(BigDecimal x, BigInteger y, BigInteger r) {
      BigDecimal bx = x;
      BigDecimal by = new BigDecimal(y);
      BigDecimal br = new BigDecimal(r);
      BigDecimal rHalf = br.divide(BigDecimal.valueOf(2));
      BigDecimal negR  = br.negate();

      if (x.signum() <= 0 && y.signum() <= 0) {
          BigDecimal sumSq = bx.multiply(bx).add(by.multiply(by));
          BigDecimal rSq = br.multiply(br);
          return sumSq.compareTo(rSq) <= 0;
      }
      if (x.signum() >= 0 && y.signum() >= 0) {
          return bx.compareTo(rHalf) <= 0 && by.compareTo(br) <= 0;
      }
      if (x.signum() >= 0 && y.signum() < 0) {
          return bx.compareTo(rHalf) <= 0 && by.compareTo(negR) >= 0;
      }
      return false;
  }

  public BigDecimal getX() {
    return x;
  }

  public BigInteger getY() {
    return y;
  }

  public BigInteger getR() {
    return r;
  }

  public boolean isInArea() {
    return isInArea;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Point point = (Point) o;
    return x == point.x && y == point.y && r == point.r;
  }

  @Override
  public int hashCode() {
    return Objects.hash(x, y, r);
  }

  @Override
  public String toString() {
    return "Point{" +
      "x=" + x +
      ", y=" + y +
      ", r=" + r +
      ", isInArea=" + isInArea +
      '}';
  }

  public abstract boolean coordsOk();

  public abstract BigInteger parseInteger(String value);
  public abstract BigDecimal parseDecimal(String value);
}