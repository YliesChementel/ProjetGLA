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

        Logger logger = Logger.getLogger(Api.class.getName());

        Api(Logger logger) {
            this.logger = logger;
        }

        public HttpRequest takeApiRequest(String requestApi) {
            return  HttpRequest.newBuilder()
                    .uri(URI.create(requestApi))
                    .header("Accept", "application/json")
                    .build();
        }

        public JSONArray takeJsonRequest(HttpRequest request, HttpClient client) throws IOException, InterruptedException {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() == 200) {
                logger.info("Statut Success");
                String body = response.body();
                JSONObject jsonResponse = new JSONObject(body);
                return jsonResponse.getJSONArray("data");
            }
            else if (response.statusCode() == 400) {
                logger.info("Erreur 400: Mauvaise requête");
            }
            else if (response.statusCode() == 500) {
                logger.info("Erreur 500: Problème serveur");
            }
            else {
                String msg = "Il y a une erreur de statut, Statut : " + response.statusCode();
                logger.info(msg);
            }
            return null;
        }


        public String takeTime() {
            DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
            LocalDateTime now = LocalDateTime.now();
            return dtf.format(now);
        }

        public void apiRun(Connection conn, HttpClient client, HttpRequest request, int nombreCrypto) throws IOException, InterruptedException {
            while (true) {
                String fetchTime = takeTime();
                JSONArray assets = takeJsonRequest(request,client);

                if(assets == null){//Pour le cas ou la connexion est rompu avec l'api
                    break;
                }

                for (int i = 0; i < nombreCrypto; i++) {
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

                Thread.sleep(1000);  // 1 seconde
            }
        }
    }
