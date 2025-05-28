package com.example.pneumoniapredictor.model

import com.google.gson.annotations.SerializedName

data class PredictionResponse(
    @SerializedName("prediction") val prediction: String,
    @SerializedName("confidence") val confidence: Double,
    @SerializedName("probability") val probability: Double
)
