package jp.ac.tut.img.oc2019.web

import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.web.bind.annotation.*
import org.springframework.web.util.UriComponentsBuilder

@Controller
@RequestMapping("/ranking")
class RankingController {
    @RequestMapping("/")
    fun index(builder: UriComponentsBuilder, model: Model): String {

        val baseUrl = builder.toUriString().replace("https", "http").replace("8443", "8000")

        model.addAttribute("faces", getRequestFacesByPictureId(baseUrl, "").body)
        return "ranking"
    }
}