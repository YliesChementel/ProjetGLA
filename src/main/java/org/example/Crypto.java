package org.example;

public class Crypto {
    private String id;
    private String symbol;
    private String name;
    private int rank;
    private double volume;
    private double price;
    private double marketCap;

    public Crypto(String id, String symbol, String name, int rank, double volume, double price, double marketCap) {
        this.id = id;
        this.symbol = symbol;
        this.name = name;
        this.rank = rank;
        this.volume = volume;
        this.price = price;
        this.marketCap = marketCap;
    }


    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public double getVolume() {
        return volume;
    }

    public void setVolume(double volume) {
        this.volume = volume;
    }

    public int getRank() {
        return rank;
    }

    public void setRank(int rank) {
        this.rank = rank;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public double getMarketCap() { return marketCap; }

    public void setMarketCap(double marketCap) { this.marketCap = marketCap; }
}
