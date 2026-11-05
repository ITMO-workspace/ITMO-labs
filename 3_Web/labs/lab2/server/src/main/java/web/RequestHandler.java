package web;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

import web.models.Point;
import web.models.RestrainedPoint;

public class RequestHandler {

    public String handle(Properties params) {
        long startTime = System.nanoTime();

        String method = params.getProperty("REQUEST_METHOD", "GET");
        if (!"GET".equalsIgnoreCase(method)) {
            return errorJson(405, "Method Not Allowed");
        }

        Map<String, String> query = parseQuery(params.getProperty("QUERY_STRING", ""));

        String rawX = query.get("x");
        String rawY = query.get("y");
        String rawR = query.get("r");

        if (rawX == null || rawY == null || rawR == null) {
            return errorJson(400, "Missing required parameters: x, y, r");
        }
        
        try {
            Point point = new RestrainedPoint(rawX, rawY, rawR);
            if (!point.coordsOk()) return errorJson(400, "Some of parameters are out of range.");

            boolean inside = point.isInArea();
            
            long endTime = System.nanoTime();
            double execTime = (endTime - startTime) / 1_000_000.0;
            String scriptTimeStr = String.format("%.2f", execTime);
            String currentTime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());

            String json = "{" +
                "\"x\":\"" + point.getX().toPlainString() + "\"," +
                "\"y\":\"" + point.getY() + "\"," +
                "\"r\":\"" + point.getR() + "\"," +
                "\"inside\":\"" + inside + "\"," +
                "\"serverTime\":\"" + currentTime + "\"," +
                "\"scriptTime\":\"" + scriptTimeStr + "\"" +
            "}";

            return httpOk(json);
        } catch (NumberFormatException e) {
            return errorJson(400, "All parameters must be numeric.");
        }

       
    }

    private static Map<String, String> parseQuery(String qs) {
        Map<String, String> map = new HashMap<>();
        if (qs == null || qs.isEmpty()) return map;
        for (String pair : qs.split("&")) {
            int eq = pair.indexOf('=');
            if (eq < 0) continue;
            String k = URLDecoder.decode(pair.substring(0, eq), StandardCharsets.UTF_8);
            String v = URLDecoder.decode(pair.substring(eq + 1), StandardCharsets.UTF_8);
            map.put(k, v);
        }
        return map;
    }

    private static String httpOk(String body) {
        return "Content-Type: application/json; charset=UTF-8\r\n" +
               "Content-Length: " + body.getBytes(StandardCharsets.UTF_8).length + "\r\n" +
               "\r\n" +
               body;
    }

    private static String errorJson(int status, String message) {
        String body = "{\"error\":\"" + message + "\"}";
        String reason = (status == 400) ? "Bad Request" : "Method Not Allowed";
        
        return "Status: " + status + " " + reason + "\r\n" +
               "Content-Type: application/json; charset=UTF-8\r\n" +
               "Content-Length: " + body.getBytes(StandardCharsets.UTF_8).length + "\r\n" +
               "\r\n" +
               body;
    }
}