package jp.ac.tut.img.oc2019.web

import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.web.bind.annotation.*
import org.springframework.web.util.UriComponentsBuilder

@Controller
@RequestMapping("/result")
class ResultController {
    @PostMapping("/")
    fun postIndex(@RequestBody result: Result, model: Model): String {
        model.addAttribute("id", result.id)
        model.addAttribute("decorated", result.decorated)
        model.addAttribute("qrcode", result.qrcode)
        return "result"
    }

    @GetMapping("/")
    fun getIndex(): String = "redirect:../"

    @GetMapping("/detail")
    fun postDetail(@RequestParam("id") id: String, builder: UriComponentsBuilder, model: Model): String {
        val baseUrl = builder.toUriString().replace("https", "http").replace("8443", "8000")

        model.addAttribute("id", id)
        model.addAttribute("faces", getRequestFacesByPictureId(baseUrl, id).body)
        model.addAttribute("picture", getRequestPicturesById(baseUrl, id).body)
        return "detail"
    }
}