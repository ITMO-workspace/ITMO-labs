package web;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import web.models.Point;

public class RequestHandler {

    public String handle(Map<String, String> params) {
        long startTime = System.nanoTime();

        String method = params.getOrDefault("REQUEST_METHOD", "GET");
        if (!"GET".equalsIgnoreCase(method)) {
            return errorJson(405, "Method Not Allowed");
        }

        String queryString = params.getOrDefault("QUERY_STRING", "");
        Map<String, String> query = parseQuery(queryString);

        String rawX = query.get("x");
        String rawY = query.get("y");
        String rawR = query.get("r");

        if (rawX == null || rawY == null || rawR == null) {
            return errorJson(400, "Missing required parameters: x, y, r");
        }

        double x, y, r;
        try {
            x = Double.parseDouble(rawX);
            y = Double.parseDouble(rawY);
            r = Double.parseDouble(rawR);
        } catch (NumberFormatException e) {
            return errorJson(400, "Parameters x, y, r must be numeric.");
        }

        Point point = new Point(x, y, r);
        boolean inside = point.isInArea();
        
        long endTime = System.nanoTime();
        double execTime = (endTime - startTime) / 1_000_000.0;
        String scriptTimeStr = String.format("%.2f", execTime);
        String currentTime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());

        String json = "{" +
            "\"x\":" + x + "," +
            "\"y\":" + y + "," +
            "\"r\":" + r + "," +
            "\"inside\":" + inside + "," +
            "\"serverTime\":\"" + currentTime + "\"," +
            "\"scriptTime\":\"" + scriptTimeStr + "\"" +
        "}";

        return httpOk(json);
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