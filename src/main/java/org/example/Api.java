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
import java.util.logging.Logger;

import static org.example.CryptoDataBase.*;

public class Api {

    static Logger logger = Logger.getLogger(Api.class.getName());

    private Api() {

    }

    static HttpRequest takeApiRequest(String requestApi) {
        return  HttpRequest.newBuilder()
                .uri(URI.create(requestApi))
                .header("Accept", "application/json")
                .build();
    }

    static JSONArray takeJsonRequest(HttpRequest request, HttpClient client) throws IOException, InterruptedException {
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        if(response.statusCode()==400) {
            logger.info("Statut Error");
        }
        if(response.statusCode()==200) {
            logger.info("Statut Success");
        }
        String body = response.body();

        JSONObject jsonResponse = new JSONObject(body);
        return jsonResponse.getJSONArray("data");
    }

    static String takeTime() {
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        LocalDateTime now = LocalDateTime.now();
        return dtf.format(now);
    }

    static void apiRun(String cryptoDB, HttpClient client, HttpRequest request) throws IOException, InterruptedException {
        while (true) {
            try (Connection conn = DriverManager.getConnection(cryptoDB)) {

                String fetchTime = takeTime();
                JSONArray assets = takeJsonRequest(request,client);

                for (int i = 0; i < 5; i++) {
                    JSONObject asset = assets.getJSONObject(i);
                    Crypto crypto = new Crypto(asset.getString("id"),
                            asset.getString("symbol"),
                            asset.getString("name"),
                            Integer.parseInt(asset.getString("rank")),
                            asset.optDouble("volumeUsd24Hr", 0.0),
                            asset.optDouble("priceUsd", 0.0));

                    insertIntoCrypto(conn, crypto.getId(), crypto.getSymbol(), crypto.getName());
                    insertIntoCryptoData(conn, crypto.getId(), crypto.getRank(), crypto.getVolume(), crypto.getPrice(), fetchTime);
                }

                displayCrypto(conn);
                displayCryptoData(conn);

            } catch (SQLException e) {
                logger.info(e.getMessage());
            }

            Thread.sleep(1000);  // 1 seconde
        }
    }
}
