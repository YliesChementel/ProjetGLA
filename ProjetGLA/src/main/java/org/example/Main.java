package org.example;

import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import static org.example.Api.apiRun;
import static org.example.Api.takeJsonRequest;
import static org.example.CryptoDataBase.*;

public class Main {
    public static void main(String[] args) throws SQLException, IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = takeJsonRequest("https://api.coincap.io/v2/assets");

        //
        String cryptoDB = "jdbc:sqlite:Crypto.db";
        try (Connection conn = DriverManager.getConnection(cryptoDB)) {
            if (!tableExists(conn, "Crypto")) {
                createCrypto(conn);
            }
            if (!tableExists(conn, "CryptoData")) {
                createCryptoData(conn);
            }
        }
        //

        apiRun( cryptoDB,  client,  request);
    }
}