/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartbin;

import java.util.ArrayList;

/**
 *
 * @author faurehu
 */
public class Users {
    
        ArrayList<String> users;
    
    public Users() {
        
        users = new ArrayList<String>();
        
    }
    
    public void addUser(String s) {
        
        users.add(s);
        
    }
    
    public ArrayList<String> getList() {
        
        return users;
        
    }
    
}
