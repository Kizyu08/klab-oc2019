package jp.ac.tut.img.oc2019.web

import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.web.bind.annotation.*

@Controller
class IndexController {
    @GetMapping("/")
    fun hello(model: Model): String = "index"

    @GetMapping("/camera")
    fun camera(model: Model) = "camera"

    @PostMapping("/confirm")
    fun postConfirm(@RequestParam("img")b64Img: String, model: Model): String {
        model.addAttribute("img", b64Img)
        return "confirm"
    }

    @PostMapping("/process")
    fun process(@RequestParam("img")b64Img: String, model: Model): String {
        model.addAttribute("img", b64Img)
        return "process"
    }
}