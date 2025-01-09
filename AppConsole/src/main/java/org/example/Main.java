package org.example;

import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.logging.Logger;

import static org.example.CryptoDataBase.*;

public class
Main {
    public static void main(String[] args) throws SQLException, IOException, InterruptedException {
        Logger logger = Logger.getLogger(Api.class.getName());
        Api api = new Api(logger);
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = api.takeApiRequest("https://api.coincap.io/v2/assets");

        //Vérification de si les tables existe
        String cryptoDB = System.getenv("DB_PATH");  // Récupère la variable d'environnement DB_PATH
        if (cryptoDB == null) {
            cryptoDB = "../instance/Crypto.db";  // Valeur par défaut si la variable d'environnement n'est pas définie
        }
        try (Connection conn = DriverManager.getConnection("jdbc:sqlite:"+cryptoDB)) {
            if (!tableExists(conn, "Crypto")) {
                createCrypto(conn);
            }
            if (!tableExists(conn, "CryptoData")) {
                createCryptoData(conn);
            }
            api.apiRun(conn, client, request,10);
        }
    }
}