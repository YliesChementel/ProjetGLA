import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpHeaders;

public class Api {
    public static void main(String[] args) {
        try {
            HttpClient client = HttpClient.newHttpClient();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.coincap.io/v2/assets"))
                    .header("Accept", "application/json")
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("Statut de la réponse: " + response.statusCode());
            System.out.println("Corps de la réponse: " + response.body());
            HttpHeaders headers = response.headers();
            headers.map().forEach((k,v) -> System.out.println(k + ":" + v));
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
