package org.example;

import org.json.JSONArray;
import org.json.JSONObject;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.sql.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Api {

    private static void createCrypto(Connection conn) {
        String sql = "CREATE TABLE IF NOT EXISTS Crypto (" +
                "id TEXT PRIMARY KEY," +
                "symbol TEXT NOT NULL," +
                "name TEXT NOT NULL);";

        try (Statement stmt = conn.createStatement()) {
            stmt.execute(sql);
            System.out.println("Table 'Crypto' créée !");
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }



    private static void insertIntoCrypto(Connection conn, String id,String symbol, String name) {
        String sql = "INSERT INTO Crypto(id, symbol, name) VALUES(?, ?, ?)";

        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, id);
            pstmt.setString(2, symbol);
            pstmt.setString(3, name);
            pstmt.executeUpdate();
            System.out.println("Données insérées : " + id + ", " + name + ", " + symbol);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void displayCrypto(Connection conn) {
        String sql = "SELECT id, symbol, name FROM Crypto";

        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            // Afficher les données
            while (rs.next()) {
                System.out.println("ID: " + rs.getString("id") + ", Symbole: " + rs.getString("symbol") + ", Nom: " + rs.getString("name"));
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }



    public static void main(String[] args) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.coincap.io/v2/assets"))
                    .header("Accept", "application/json")
                    .build();

            String cryptoDB = "jdbc:sqlite:Crypto.db";
            String cryptoDataDB = "jdbc:sqlite:CryptoData.db";
            try (Connection conn = DriverManager.getConnection(cryptoDB)) {
                createCrypto(conn);
            }
            catch (SQLException e) {
                System.out.println(e.getMessage());
            }
            while (true) {
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                System.out.println("Statut de la réponse: " + response.statusCode());
                String body = response.body();

                JSONObject jsonResponse = new JSONObject(body);
                JSONArray assets = jsonResponse.getJSONArray("data");

                DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
                LocalDateTime now = LocalDateTime.now();
                System.out.println(dtf.format(now));


                try (Connection conn = DriverManager.getConnection(cryptoDB)) {
                    for(int i=0; i<5; i++) {
                        String bitcoinId = assets.getJSONObject(i).getString("id");
                        String bitcoinRank = assets.getJSONObject(i).getString("rank");
                        String bitcoinSymbol = assets.getJSONObject(i).getString("symbol");
                        String bitcoinName = assets.getJSONObject(i).getString("name");
                        String bitcoinVolume = assets.getJSONObject(i).getString("volumeUsd24Hr");
                        String bitcoinPrice = assets.getJSONObject(i).getString("priceUsd");
                        if (conn != null) {
                            insertIntoCrypto(conn, bitcoinId, bitcoinSymbol,bitcoinName);
                            displayCrypto(conn);
                        }
                    }
                } catch (SQLException e) {
                    System.out.println(e.getMessage());
                }

            Thread.sleep(20000);  // 30 secondes
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
