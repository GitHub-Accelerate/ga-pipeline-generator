package main

import (
	"context"

	"dagger/hello-dagger/internal/dagger"
)

type HelloDagger struct{}

// Publish the application container after building and testing it on-the-fly
func (m *HelloDagger) Publish(
	ctx context.Context,
	// +defaultPath="/"
	source *dagger.Directory,
) (string, error) {
	_, err := m.Test(ctx, source)
	if err != nil {
		return "", err
	}
	buildOutput, err2 := m.Build(ctx, source)
	if err2 != nil {
		return "", err2
	}
	return buildOutput, nil
	//m.Publish(ctx, fmt.Sprintf("ttl.sh/hello-dagger-%.0f", math.Floor(rand.Float64()*10000000))) //#nosec
}

// Build the application container
func (m *HelloDagger) Build(
	ctx context.Context,
	// +defaultPath="/"
	source *dagger.Directory,
) (string, error) {
	return m.BuildEnv(source).
		WithExec([]string{"go", "build", "main.go"}). // Build your Go program
		Stdout(ctx)
}

// Return the result of running unit tests
func (m *HelloDagger) Test(
	ctx context.Context,
	// +defaultPath="/"
	source *dagger.Directory,
) (string, error) {
	return m.BuildEnv(source).
		WithExec([]string{"go", "test"}).
		Stdout(ctx)
}

// Build a ready-to-use development environment
func (m *HelloDagger) BuildEnv(
	// +defaultPath="/"
	source *dagger.Directory,
) *dagger.Container {
	goCache := dag.CacheVolume("golang")
	return dag.Container().
		From("golang:latest").
		WithDirectory("/src", source).
		WithMountedCache("/go/pkg/mod", goCache).
		WithWorkdir("/src").
		WithExec([]string{"go", "mod", "download"})
}
