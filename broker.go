package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"runtime/pprof"
	"github.com/surge/glog"
	"github.com/surgemq/surgemq/service"
)

var (
	cpuprofile       string
)

func main() {
	fmt.Println("hi")
	svr := &service.Server{
		KeepAlive:        300,           // seconds
		ConnectTimeout:   2,             // seconds
		SessionsProvider: "mem",         // keeps sessions in memory
		Authenticator:    "mockSuccess", // always succeed
		TopicsProvider:   "mem",         // keeps topic subscriptions in memory
	}

	var f *os.File
	var err error

	if cpuprofile != "" {
		f, err = os.Create(cpuprofile)
		if err != nil {
			log.Fatal(err)
		}

		pprof.StartCPUProfile(f)
	}

	sigchan := make(chan os.Signal, 1)
	signal.Notify(sigchan, os.Interrupt, os.Kill)
	go func() {
		sig := <-sigchan
		glog.Errorf("Existing due to trapped signal; %v", sig)

		if f != nil {
			glog.Errorf("Stopping profile")
			pprof.StopCPUProfile()
			f.Close()
		}

		svr.Close()

		os.Exit(0)
	}()

	err = svr.ListenAndServe("tcp://:1883")
	if err != nil {
		glog.Errorf("surgemq/main: %v", err)
	}

}
