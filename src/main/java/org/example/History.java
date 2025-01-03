package org.example;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.sql.*;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.TimeZone;
import java.util.logging.Logger;

import static org.example.CryptoDataBase.*;

public class History {
    public static void main(String[] args) throws SQLException, IOException, InterruptedException {
        String cryptoDB = "jdbc:sqlite:instance/Crypto.db";

        String[] listInterval={"d1","h6","h1","m15","m1"};
        String[] listBitcoin={"bitcoin","ethereum","tether","binance-coin","xrp","solana","dogecoin","usd-coin","steth","cardano"};
        for(int k = 0;k<listBitcoin.length;k++) {
            for (int j = 0; j < listInterval.length; j++) {
                Api api = new Api(logger);
                HttpClient client = HttpClient.newHttpClient();
                HttpRequest requestHistory = api.takeApiRequest("https://api.coincap.io/v2/assets/"+listBitcoin[k]+"/history?interval=" + listInterval[j]);

                HttpResponse<String> response = client.send(requestHistory, HttpResponse.BodyHandlers.ofString());
                if (response.statusCode() == 200) {
                    String body = response.body();
                    JSONObject jsonResponse = new JSONObject(body);
                    JSONArray assets = jsonResponse.getJSONArray("data");
                    for (int i = 0; i < assets.length(); i++) {
                        JSONObject asset = assets.getJSONObject(i);

                        long timestampInSeconds = asset.getLong("time") / 1000;

                        // Créer un objet Date à partir du timestamp (en millisecondes)
                        Date date = new Date(timestampInSeconds * 1000);

                        // Formater la date au format souhaité avec fuseau horaire UTC
                        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                        sdf.setTimeZone(TimeZone.getTimeZone("UTC")); // Définir le fuseau horaire UTC
                        String formattedTime = sdf.format(date);
                        //System.out.println("Price: " + asset.getString("priceUsd") + " Temps: " + formattedTime);


                        try (Connection conn = DriverManager.getConnection(cryptoDB)) {
                            String sqlInsert = "INSERT INTO CryptoHistory(crypto_id, price,fetchTime) VALUES(?, ?, ?)";
                            String crypto_id = listBitcoin[k];
                            String price = asset.getString("priceUsd");
                            String timeInterval = listInterval[j];
                            try (PreparedStatement pstmt = conn.prepareStatement(sqlInsert)) {
                                pstmt.setString(1, crypto_id);
                                pstmt.setString(2, price);
                                pstmt.setString(4, formattedTime);
                                pstmt.executeUpdate();
                                String msg = "Données insérées dans 'CryptoHistory': " + crypto_id + ", " + price + ", " + ", " + formattedTime;
                                //System.out.println(msg);
                            } catch (SQLException ignored) {
                            }
                        }

                /*String sql = "CREATE TABLE IF NOT EXISTS CryptoHistory (" +
                        "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                        "crypto_id TEXT NOT NULL," +
                        "price DECIMAL(30,20)," +
                        "fetchTime TIMESTAMP NOT NULL," +
                        "FOREIGN KEY(crypto_id) REFERENCES Crypto(id));";

                try (Statement stmt = conn.createStatement()) {
                    stmt.execute(sql);
                } catch (SQLException ignored) {
                }*/
                    }
                }
            }
        }



    }
}
