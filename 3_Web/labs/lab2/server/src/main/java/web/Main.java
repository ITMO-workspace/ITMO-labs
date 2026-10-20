package web;

import com.fastcgi.FCGIInterface;
import java.util.HashMap;
import java.util.Map;

/**
* Main class
* @author Septyq
*/

public class Main {

    public static void main(String[] args) {
        var fcgiInterface = new FCGIInterface();
        var handler = new RequestHandler();

        while (fcgiInterface.FCGIaccept() >= 0) {
            try {
                Map<String, String> params = collectParams();
                
                String response = handler.handle(params);
                
                System.out.println(response);
                
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println("HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: 21\r\n\r\nInternal Server Error");
            }
        }
    }

    private static Map<String, String> collectParams() {
        Map<String, String> map = new HashMap<>();
        var params = FCGIInterface.request.params;
        if (params == null) return map;

        // Iterate over the Properties object
        for (String key : params.stringPropertyNames()) {
            map.put(key, params.getProperty(key));
        }
        return map;
    }
}