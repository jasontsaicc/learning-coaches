package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"strings"
	"time"
)

var secret = []byte("super-secret-key")

type Header struct {
	Alg string `json:"alg"`
	Typ string `json:"typ"`
}

type Claims struct {
	Sub string `json:"sub"`
	Exp int64  `json:"exp"`
	Iat int64  `json:"iat"`
}

func b64(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func issueToken(userID string) string {
	headerJSON, _ := json.Marshal(Header{Alg: "HS256", Typ: "JWT"})
	claimsJSON, _ := json.Marshal(Claims{
		Sub: userID,
		Iat: time.Now().Unix(),
		Exp: time.Now().Add(15 * time.Minute).Unix(),
	})

	headerB64 := b64(headerJSON)
	claimsB64 := b64(claimsJSON)
	signingInput := headerB64 + "." + claimsB64

	mac := hmac.New(sha256.New, secret)
	mac.Write([]byte(signingInput))
	sig := b64(mac.Sum(nil))

	return signingInput + "." + sig
}

func validateToken(token string) (string, error) {
	// Step 1: split
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return "", fmt.Errorf("invalid token format")
	}

	// Step 2: re-compute signature, compare in constant time
	signingInput := parts[0] + "." + parts[1]
	mac := hmac.New(sha256.New, secret)
	mac.Write([]byte(signingInput))
	expectedSig := b64(mac.Sum(nil))
	if !hmac.Equal([]byte(expectedSig), []byte(parts[2])) {
		return "", fmt.Errorf("invalid signature")
	}

	// Step 3: decode payload
	payloadBytes, err := base64.RawURLEncoding.DecodeString(parts[1])
	if err != nil {
		return "", fmt.Errorf("invalid payload encoding")
	}
	var claims Claims
	if err := json.Unmarshal(payloadBytes, &claims); err != nil {
		return "", fmt.Errorf("invalid payload json")
	}

	// Step 4: check expiry
	if time.Now().Unix() > claims.Exp {
		return "", fmt.Errorf("token expired")
	}

	// Step 5: return userID
	return claims.Sub, nil
}

func main() {
	token := issueToken("user-42")
	fmt.Println("=== Issued Token ===")
	parts := strings.Split(token, ".")
	fmt.Printf("Header:    %s\n", parts[0])
	fmt.Printf("Payload:   %s\n", parts[1])
	fmt.Printf("Signature: %s\n", parts[2])
	fmt.Println()

	userID, err := validateToken(token)
	if err != nil {
		fmt.Printf("Validation failed: %v\n", err)
		return
	}
	fmt.Printf("Valid token. UserID: %s\n", userID)

	// tamper test: flip one character in the payload
	tampered := parts[0] + "." + parts[1] + "x" + "." + parts[2]
	_, err = validateToken(tampered)
	fmt.Printf("Tampered token result: %v\n", err)
}
