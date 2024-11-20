package org.example;

import org.json.JSONArray;
import org.json.JSONObject;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

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

                for(int i=0; i<5; i++) {
                    String bitcoinId = assets.getJSONObject(i).getString("id");
                    System.out.println(bitcoinId);
                    String bitcoinRank = assets.getJSONObject(i).getString("rank");
                    System.out.println(bitcoinRank);
                    String bitcoinSymbol = assets.getJSONObject(i).getString("symbol");
                    System.out.println(bitcoinSymbol);
                    String bitcoinName = assets.getJSONObject(i).getString("name");
                    System.out.println(bitcoinName);
                    String bitcoinVolume = assets.getJSONObject(i).getString("volumeUsd24Hr");
                    System.out.println(bitcoinVolume);
                    String bitcoinPrice = assets.getJSONObject(i).getString("priceUsd");
                    System.out.println(bitcoinPrice);
                }
                DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
                LocalDateTime now = LocalDateTime.now();
                System.out.println(dtf.format(now));

                Thread.sleep(30000);  // 30 secondes
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
