//
//  DropBox.swift
//  kutapada-ios
//
//  Created by Dr. Kerem Koseoglu on 29.03.2020.
//  Copyright © 2020 Dr. Kerem Koseoglu. All rights reserved.
//

import Foundation
import UIKit

class DropBox {
    private var APP_KEY = "cf3j7hgw2kp4uk9"
    private var TOKEN_KEY = "token"
    private var defaults = UserDefaults.standard
    private var _passwordFileContent = ""

    var passwordFileContent: String {
        get { return self._passwordFileContent }
    }
    
    var token: String {
        get {
            return defaults.string(forKey: TOKEN_KEY) ?? ""
        }
        set(newToken) {
            defaults.set(newToken, forKey: TOKEN_KEY)
        }
    }
    
    func authorize() {
        let url = URL(string: "https://www.dropbox.com/oauth2/authorize?client_id=" + APP_KEY + "&response_type=code")!
        
        UIApplication.shared.open(
            url,
            options: [:],
            completionHandler: {
                (success) in print("Open URL success")})
    }
    
    func readPasswordFileContent() {
        _passwordFileContent = ""
        let url = URL(string: "https://content.dropboxapi.com/2/files/download")!
        let currentToken = token
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        print(currentToken)
        request.addValue("Bearer " + currentToken, forHTTPHeaderField: "Authorization")
        request.addValue("{\"path\": \"/kutapada.json\"}", forHTTPHeaderField: "Dropbox-API-Arg")
        
        URLSession.shared.dataTask(with: request) { (data, response, error) in
            guard error == nil else { print(error!.localizedDescription); return }
            guard let data = data else { print("Empty data"); return }

            if let str = String(data: data, encoding: .utf8) {
                self._passwordFileContent = str
            }
        }.resume()
    }

}
