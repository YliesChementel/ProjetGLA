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

    private static void createCryptoData(Connection conn) {
        String sql = "CREATE TABLE IF NOT EXISTS CryptoData (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "crypto_id TEXT NOT NULL," +
                "rank INTEGER NOT NULL," +
                "volume DECIMAL(30,10)," +
                "price DECIMAL(30,10)," +
                "fetchTime TIMESTAMP NOT NULL," +
                "FOREIGN KEY(crypto_id) REFERENCES Crypto(id));";

        try (Statement stmt = conn.createStatement()) {
            stmt.execute(sql);
            System.out.println("Table 'CryptoData' créée !");
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    private static boolean tableExists(Connection conn, String tableName) {
        try (ResultSet rs = conn.getMetaData().getTables(null, null, tableName, null)) {
            return rs.next();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return false;
        }
    }

    private static void insertIntoCrypto(Connection conn, String id,String symbol, String name) {
        String sql = "INSERT INTO Crypto(id, symbol, name) VALUES(?, ?, ?)" + "ON CONFLICT(id) DO NOTHING";

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

    private static void insertIntoCryptoData(Connection conn, String cryptoId, int rank, double volume, double price, String fetchTime) {
        String sql = "INSERT INTO CryptoData(crypto_id, rank, volume, price, fetchTime) VALUES(?, ?, ?, ?, ?)";

        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, cryptoId);
            pstmt.setInt(2, rank);
            pstmt.setDouble(3, volume);
            pstmt.setDouble(4, price);
            pstmt.setString(5, fetchTime);
            pstmt.executeUpdate();
            System.out.println("Données insérées dans 'CryptoData': " + cryptoId + ", " + rank + ", " + volume + ", " + price + ", " + fetchTime);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void displayCrypto(Connection conn) {
        String sql = "SELECT id, symbol, name FROM Crypto";

        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            while (rs.next()) {
                System.out.println("ID: " + rs.getString("id") + ", Symbole: " + rs.getString("symbol") + ", Nom: " + rs.getString("name"));
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void displayCryptoData(Connection conn) {
        String sql = "SELECT id, crypto_id, rank, volume, price, fetchTime FROM CryptoData";

        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            while (rs.next()) {
                System.out.println("ID: " + rs.getString("id") + ", CryptoId: " + rs.getString("crypto_id") + ", Rank: " + rs.getString("rank") + ", Volume: " + rs.getString("volume") + ", Price: " + rs.getString("price") + ", FetchTime: " + rs.getString("fetchTime"));
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
                if (!tableExists(conn, "Crypto")) {
                    createCrypto(conn);
                }
            }

            try (Connection conn2 = DriverManager.getConnection(cryptoDataDB)) {
                if (!tableExists(conn2, "CryptoData")) {
                    createCryptoData(conn2);
                }
            }
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

                try (Connection conn = DriverManager.getConnection(cryptoDB);
                     Connection conn2 = DriverManager.getConnection(cryptoDataDB)) {

                    for (int i = 0; i < 5; i++) {
                        JSONObject asset = assets.getJSONObject(i);

                        String id = asset.getString("id");
                        String symbol = asset.getString("symbol");
                        String name = asset.getString("name");
                        int rank = Integer.parseInt(asset.getString("rank"));
                        double volume = asset.optDouble("volumeUsd24Hr", 0.0);
                        double price = asset.optDouble("priceUsd", 0.0);

                        insertIntoCrypto(conn, id, symbol, name);
                        insertIntoCryptoData(conn2, id, rank, volume, price, fetchTime);
                    }

                    displayCrypto(conn);
                    displayCryptoData(conn2);
                } catch (SQLException e) {
                    System.out.println(e.getMessage());
                }

            Thread.sleep(10000);  // 20 secondes
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
