(ns birding
  (:use     [streamparse.specs])
  (:gen-class))

(defn birding [options]
  [
    ;; spout configuration
    {"term-spout" (python-spout-spec
          options
          ; Dispatch class based on birding.yml.
          "birding.spout.DispatchSpout"
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
     "elasticsearch-index-bolt" (python-bolt-spec
          options
          {"lookup-bolt" :shuffle}
          "birding.bolt.ElasticsearchIndexBolt"
          []
          :p 1
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
