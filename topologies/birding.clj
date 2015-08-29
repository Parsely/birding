(ns birding
  (:use     [streamparse.specs])
  (:gen-class))

(defn birding [options]
  [
    ;; spout configuration
    {"term-spout" (python-spout-spec
          options
          "birding.spout.SimpleSimulationSpout"
          ["term" "timestamp"]
          )
    }
    ;; bolt configuration
    {"search-bolt" (python-bolt-spec
          options
          ; Use field grouping on term to support in-memory caching.
          {"term-spout" ["term"]}
          "birding.bolt.TwitterSearchBolt"
          ["term" "timestamp" "search_result"]
          :p 2
          )
     "lookup-bolt" (python-bolt-spec
          options
          {"search-bolt" :shuffle}
          "birding.bolt.TwitterLookupBolt"
          ["term" "timestamp" "lookup_result"]
          :p 2
          )
     "result-topic-bolt" (python-bolt-spec
          options
          {"lookup-bolt" :shuffle}
          "birding.bolt.ResultTopicBolt"
          []
          :p 1
          )
    }
  ]
)
