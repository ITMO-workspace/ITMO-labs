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
                String response = handler.handle(FCGIInterface.request.params);
                
                System.out.print(response);
                System.out.flush();
                
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}