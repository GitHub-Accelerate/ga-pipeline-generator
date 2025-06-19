package main

import "testing"

func TestGetHello(t *testing.T) {
	expected := "Hello, world!"
	result := GetHello()
	if result != expected {
		t.Errorf("GetHello() = %q; want %q", result, expected)
	}
}
