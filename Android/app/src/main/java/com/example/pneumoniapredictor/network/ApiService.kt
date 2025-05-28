package com.example.pneumoniapredictor.network

import com.example.pneumoniapredictor.model.PredictionResponse
import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface ApiService {
    @Multipart
    @POST("predict")
    suspend fun predictPneumonia(
        @Part file: MultipartBody.Part
    ): Response<PredictionResponse>
}