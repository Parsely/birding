(ns birding
  (:use     [streamparse.specs])
  (:gen-class))

(defn birding [options]
  [
    ;; spout configuration
    {"url-spout" (python-spout-spec
          options
          "birding.spout.SimpleSimulationSpout"
          ["url" "timestamp"]
          )
    }
    ;; bolt configuration
    {"search-bolt" (python-bolt-spec
          options
          ; Use field grouping on URL to support in-memory caching.
          {"url-spout" ["url"]}
          "birding.bolt.TwitterSearchBolt"
          ["url" "timestamp" "search_result"]
          :p 2
          )
     "lookup-bolt" (python-bolt-spec
          options
          {"search-bolt" :shuffle}
          "birding.bolt.TwitterLookupBolt"
          ["url" "timestamp" "lookup_result"]
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
