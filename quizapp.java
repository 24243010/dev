import com.sun.net.httpserver.*;
import java.net.*;
import java.io.*;

public class QuizApp {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(
            new InetSocketAddress(8080), 0
        );

        server.createContext("/score", exchange -> {
            String answer = new String(
                exchange.getRequestBody().readAllBytes()
            );

            String result = answer.equals("B")
                ? "{\"score\":1}"
                : "{\"score\":0}";

            byte[] data = result.getBytes();

            exchange.getResponseHeaders().set(
                "Content-Type", "application/json"
            );

            exchange.sendResponseHeaders(200, data.length);
            exchange.getResponseBody().write(data);
            exchange.close();
        });

        server.createContext("/", exchange -> {
            byte[] data = java.nio.file.Files.readAllBytes(
                java.nio.file.Paths.get("index.html")
            );

            exchange.getResponseHeaders().set(
                "Content-Type", "text/html"
            );

            exchange.sendResponseHeaders(200, data.length);
            exchange.getResponseBody().write(data);
            exchange.close();
        });

        server.start();
        System.out.println("Quiz App Started!");
        System.out.println("Open http://localhost:8080");
    }
}
