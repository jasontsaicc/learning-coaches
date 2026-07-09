package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"

	_ "github.com/lib/pq"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

type Product struct {
	ID         int
	Name       string
	Category   string
	Price      float64
	Attributes map[string]string
}

func sampleProducts() []Product {
	return []Product{
		{ID: 1, Name: "iPhone 15 Pro", Category: "electronics", Price: 999.99,
			Attributes: map[string]string{"brand": "Apple", "screen": "6.1in"}},
		{ID: 2, Name: "Galaxy S24", Category: "electronics", Price: 799.99,
			Attributes: map[string]string{"brand": "Samsung", "screen": "6.2in"}},
		{ID: 3, Name: "MacBook Air M3", Category: "electronics", Price: 1099.00,
			Attributes: map[string]string{"brand": "Apple", "ram": "8GB"}},
		{ID: 4, Name: "Running Shoes", Category: "sports", Price: 129.99,
			Attributes: map[string]string{"brand": "Nike", "size": "10"}},
		{ID: 5, Name: "Yoga Mat", Category: "sports", Price: 49.99,
			Attributes: map[string]string{"brand": "Lululemon", "color": "purple"}},
	}
}

func main() {
	ctx := context.TODO()
	products := sampleProducts()

	// --- Postgres ---
	pgConn := "postgres://demo:demo123@localhost:5432/productdb?sslmode=disable"
	db, err := sql.Open("postgres", pgConn)
	if err != nil {
		log.Fatal("PG open:", err)
	}
	defer db.Close()
	if err := db.PingContext(ctx); err != nil {
		log.Fatal("PG ping:", err)
	}
	fmt.Println("Postgres connected")

	// --- MongoDB ---
	mgClient, err := mongo.Connect(options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		log.Fatal("Mongo connect:", err)
	}
	defer mgClient.Disconnect(ctx)
	fmt.Println("MongoDB connected")

	// --- Postgres: Create table + Insert ---
	insertPostgres(ctx, db, products)

	// --- MongoDB: Insert ---
	mgColl := mgClient.Database("productdb").Collection("products")
	insertMongo(ctx, mgColl, products)

	// --- Query Comparison ---
	fmt.Println("\n========== QUERY COMPARISON ==========")

	// Query 1: Structured field — both DBs handle well
	fmt.Println("\n--- Query 1: Electronics under $1000 ---")
	queryByCategory(ctx, db, mgColl)

	// Query 2: Flexible attribute — this is where it gets interesting
	fmt.Println("\n--- Query 2: Brand = Apple ---")
	queryByAttribute(ctx, db, mgColl)

	fmt.Println("\nDone!")
}

// insertPostgres creates the table (with JSONB for flexible attrs) and inserts products.
func insertPostgres(ctx context.Context, db *sql.DB, products []Product) {
	// Step 1: Create table — Attributes becomes JSONB because SQL has no native map type
	_, err := db.ExecContext(ctx, `
		DROP TABLE IF EXISTS products;
		CREATE TABLE products (
			id         INT PRIMARY KEY,
			name       TEXT NOT NULL,
			category   TEXT NOT NULL,
			price      NUMERIC(10,2) NOT NULL,
			attributes JSONB DEFAULT '{}'
		)
	`)
	if err != nil {
		log.Fatal("PG create table:", err)
	}
	fmt.Println("PG: table created")

	// Step 2: Insert each product — must convert map to JSON manually
	for _, p := range products {
		attrJSON, _ := json.Marshal(p.Attributes)
		_, err := db.ExecContext(ctx,
			`INSERT INTO products (id, name, category, price, attributes)
			 VALUES ($1, $2, $3, $4, $5)`,
			p.ID, p.Name, p.Category, p.Price, string(attrJSON),
		)
		if err != nil {
			log.Fatal("PG insert:", err)
		}
	}
	fmt.Printf("PG: inserted %d products\n", len(products))
}

// insertMongo inserts products directly — no schema, no JSON conversion needed.
func insertMongo(ctx context.Context, coll *mongo.Collection, products []Product) {
	coll.Drop(ctx) // clean slate, like DROP TABLE IF EXISTS

	for _, p := range products {
		_, err := coll.InsertOne(ctx, p)
		if err != nil {
			log.Fatal("Mongo insert:", err)
		}
	}
	fmt.Printf("Mongo: inserted %d products\n", len(products))
}

// Query 1: Find electronics under $1000 — structured fields, both DBs are fine
func queryByCategory(ctx context.Context, db *sql.DB, coll *mongo.Collection) {
	// --- Postgres: standard WHERE clause ---
	fmt.Println("[PG] SELECT * FROM products WHERE category='electronics' AND price < 1000")
	rows, err := db.QueryContext(ctx,
		`SELECT id, name, price FROM products WHERE category = $1 AND price < $2`,
		"electronics", 1000,
	)
	if err != nil {
		log.Fatal("PG query:", err)
	}
	defer rows.Close()
	for rows.Next() {
		var id int
		var name string
		var price float64
		rows.Scan(&id, &name, &price)
		fmt.Printf("  [PG] id=%d name=%-20s price=%.2f\n", id, name, price)
	}

	// --- MongoDB: filter document ---
	fmt.Println("[Mongo] Find({category: 'electronics', price: {$lt: 1000}})")
	cursor, err := coll.Find(ctx, map[string]interface{}{
		"category": "electronics",
		"price":    map[string]interface{}{"$lt": 1000},
	})
	if err != nil {
		log.Fatal("Mongo query:", err)
	}
	defer cursor.Close(ctx)
	for cursor.Next(ctx) {
		var p Product
		cursor.Decode(&p)
		fmt.Printf("  [Mongo] id=%d name=%-20s price=%.2f\n", p.ID, p.Name, p.Price)
	}
}

// Query 2: Find products by flexible attribute (brand=Apple) — the key difference
func queryByAttribute(ctx context.Context, db *sql.DB, coll *mongo.Collection) {
	// --- Postgres: must use JSONB operator ->> to dig into the JSON ---
	fmt.Println("[PG] SELECT * FROM products WHERE attributes->>'brand' = 'Apple'")
	rows, err := db.QueryContext(ctx,
		`SELECT id, name, price FROM products WHERE attributes->>'brand' = $1`,
		"Apple",
	)
	if err != nil {
		log.Fatal("PG query:", err)
	}
	defer rows.Close()
	for rows.Next() {
		var id int
		var name string
		var price float64
		rows.Scan(&id, &name, &price)
		fmt.Printf("  [PG] id=%d name=%-20s price=%.2f\n", id, name, price)
	}

	// --- MongoDB: just dot into the nested field, natural ---
	fmt.Println("[Mongo] Find({attributes.brand: 'Apple'})")
	cursor, err := coll.Find(ctx, map[string]interface{}{
		"attributes.brand": "Apple",
	})
	if err != nil {
		log.Fatal("Mongo query:", err)
	}
	defer cursor.Close(ctx)
	for cursor.Next(ctx) {
		var p Product
		cursor.Decode(&p)
		fmt.Printf("  [Mongo] id=%d name=%-20s price=%.2f\n", p.ID, p.Name, p.Price)
	}
}
