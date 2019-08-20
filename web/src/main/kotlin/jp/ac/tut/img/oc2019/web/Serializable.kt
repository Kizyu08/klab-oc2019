package jp.ac.tut.img.oc2019.web

import java.io.Serializable
import kotlin.properties.Delegates

class Face: Serializable {
    var picture_id: Int by Delegates.notNull()
    lateinit var position: String
    var score: Int by Delegates.notNull()
}

class Picture: Serializable {
    var origin: String by Delegates.notNull()
    var decorated: String by Delegates.notNull()
    var qrcode: String by Delegates.notNull()
}

class Result: Serializable {
    val id: Int? = null
    val decorated: String? = null
    val qrcode: String? = null
}