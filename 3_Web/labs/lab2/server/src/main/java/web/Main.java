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
                
                System.out.print(response);
                System.out.flush();
                
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private static Map<String, String> collectParams() {
        Map<String, String> map = new HashMap<>();
        var params = FCGIInterface.request.params;
        if (params == null) return map;

        for (String key : params.stringPropertyNames()) {
            map.put(key, params.getProperty(key));
        }
        return map;
    }
}