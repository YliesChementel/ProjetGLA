package org.example;

import org.json.JSONArray;
import org.json.JSONObject;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Api {
    public static void main(String[] args) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.coincap.io/v2/assets"))
                    .header("Accept", "application/json")
                    .build();

            while (true) {
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                System.out.println("Statut de la réponse: " + response.statusCode());
                String body = response.body();

                JSONObject jsonResponse = new JSONObject(body);
                JSONArray assets = jsonResponse.getJSONArray("data");

                String nomBitcoin = assets.getJSONObject(0).getString("name");
                System.out.println("Nom du Bitcoin: " + nomBitcoin);

                Thread.sleep(30000);  // 30 secondes
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
