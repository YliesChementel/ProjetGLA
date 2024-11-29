package org.example;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.sql.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import static org.example.CryptoDataBase.*;

public class Api {


    static HttpRequest takeJsonRequest(String requestApi) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(requestApi))
                .header("Accept", "application/json")
                .build();
        return request;
    }



    static void apiRun(String cryptoDB, HttpClient client, HttpRequest request) throws IOException, InterruptedException {
        while (true) {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println("Statut de la réponse: " + response.statusCode());
            String body = response.body();

            JSONObject jsonResponse = new JSONObject(body);
            JSONArray assets = jsonResponse.getJSONArray("data");

            DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
            LocalDateTime now = LocalDateTime.now();
            String fetchTime = dtf.format(now);
            System.out.println(fetchTime);

            try (Connection conn = DriverManager.getConnection(cryptoDB)) {

                for (int i = 0; i < 5; i++) {
                    JSONObject asset = assets.getJSONObject(i);

                    String id = asset.getString("id");
                    String symbol = asset.getString("symbol");
                    String name = asset.getString("name");
                    int rank = Integer.parseInt(asset.getString("rank"));
                    double volume = asset.optDouble("volumeUsd24Hr", 0.0);
                    double price = asset.optDouble("priceUsd", 0.0);

                    insertIntoCrypto(conn, id, symbol, name);
                    insertIntoCryptoData(conn, id, rank, volume, price, fetchTime);
                }

                displayCrypto(conn);
                displayCryptoData(conn);
            } catch (SQLException e) {
                System.out.println(e.getMessage());
            }

            Thread.sleep(1000);  // 1 seconde
        }
    }
}
