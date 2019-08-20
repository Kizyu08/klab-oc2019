package jp.ac.tut.img.oc2019.web

import org.springframework.core.ParameterizedTypeReference
import org.springframework.http.RequestEntity
import org.springframework.http.ResponseEntity
import org.springframework.web.client.RestTemplate
import java.net.URI


fun <T> typeReference() = object: ParameterizedTypeReference<T>() {}

fun getRequestFacesByPictureId(url: String, pictureId: String): ResponseEntity<List<Face>> {
    val restTemplate = RestTemplate()
    val requestEntity = RequestEntity
            .get(URI("$url/api/faces/?picture_id=$pictureId"))
            .build()
    return restTemplate.exchange(requestEntity, typeReference<List<Face>>())
}

fun getRequestPicturesById(url: String, pictureId: String): ResponseEntity<Picture> {
    val restTemplate = RestTemplate()
    val requestEntity = RequestEntity
            .get(URI("$url/api/pictures/$pictureId"))
            .build()
    return restTemplate.exchange(requestEntity, typeReference<Picture>())
}