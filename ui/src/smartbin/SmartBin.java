/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package smartbin;

import javax.swing.*;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.awt.Dimension;

/**
 *
 * @author faurehu
 */
public class SmartBin {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
       
        DefaultComboBoxModel listModel = new DefaultComboBoxModel();
        listModel.removeAllElements();
        
        JFrame frame = new JFrame();
        frame.setSize(5000, 5000);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        
        JButton show = new JButton("Show");
        JButton delete = new JButton("Delete");
        JButton tag  = new JButton("Tag");
        JComboBox users = new JComboBox(listModel);
        users.setPreferredSize(new Dimension(200, 25));
        JButton add = new JButton("Add user");
        JTextField newUser = new JTextField();
        newUser.setPreferredSize(new Dimension(200, 25));
        
        frame.setLayout(new BorderLayout());
        JPanel top = new JPanel();
        top.setLayout(new FlowLayout());
        JPanel bottom = new JPanel();
        bottom.setLayout(new FlowLayout());
        JPanel center = new JPanel();
        center.setLayout(new GridLayout());
        
        frame.add(top, BorderLayout.NORTH);
        frame.add(bottom, BorderLayout.SOUTH);
        frame.add(center, BorderLayout.CENTER);
        
        top.add(users); top.add(show); top.add(tag); top.add(delete);
        bottom.add(add); bottom.add(newUser);
               
        add.addActionListener( new ActionListener() {

            @Override
            public void actionPerformed(ActionEvent e) {
                if(e.getSource().equals(add)) {
                    users.addItem(newUser.getText());
                }
            } 
            
        });
        
        frame.pack();
        frame.setVisible(true);
        
    }
    
    public static void populateGrid(String s) {
        
        
        
    }
    
}
