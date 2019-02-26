package function

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"time"
)

var looping = true

// Handle a serverless request
func Handle(req []byte) string {
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)

	mi, _ := strconv.ParseFloat(os.Getenv("mi"), 1.0)
	v := r1.ExpFloat64() / mi

	milliseconds := time.Duration(v * 1000)

	timer := time.NewTimer(milliseconds * time.Millisecond)
	go func() {
		<-timer.C
		looping = false
	}()

	startTime := time.Now()
	// test loop time
	for {
		if !looping {
			break
		}
		rand.Float64()
	}
	elapsed := time.Since(startTime)

	return fmt.Sprintf("mi = %.2f\nalfa = %.2f\nelapsed time = %.4f", mi, v, elapsed.Seconds())
}
